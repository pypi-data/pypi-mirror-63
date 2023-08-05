from itertools import imap
import idaapi
import idautils
import idc
from .base import get_func, demangle
from ..core import set_name, get_ea, fix_addresses, is_same_function,add_func
from .line import Line
from .xref import Xref
from ..ui import updates_ui
from .. import exceptions


class Comments(object):
    """IDA Function Comments

    Provides easy access to all types of comments for an IDA Function.
    """

    def __init__(self, function):
        self._function = function

    def __nonzero__(self):
        return any((self.regular, self.repeat,))

    @property
    def regular(self):
        """Function Comment"""
        return idaapi.get_func_cmt(self._function._func, False)

    @regular.setter
    def regular(self, comment):
        idaapi.set_func_cmt(self._function._func, comment, False)

    @property
    def repeat(self):
        """Repeatable Function Comment"""
        return idaapi.get_func_cmt(self._function._func, True)

    @repeat.setter
    def repeat(self, comment):
        idaapi.set_func_cmt(self._function._func, comment, True)

    def __repr__(self):
        return ("Comments("
                "func={name},"
                " reqular={regular},"
                " repeat={repeat})").format(
            name=self._function.name,
            regular=repr(self.regular),
            repeat=repr(self.repeat))


class FunctionFlagsMixin(object):
    """ Mixin to add convenience checks for the function flags provided by IDA.

    IDA SDK documentation for the flags is found at:
    https://www.hex-rays.com/products/ida/support/sdkdoc/group___f_u_n_c__.html
    """

    flags = None

    @property
    def is_noret(self):
        """ Function doesn't return """
        return bool(self.flags & idaapi.FUNC_NORET)  # 0x00000001

    @property
    def is_far(self):
        """ Is a far function. """
        return bool(self.flags & idaapi.FUNC_FAR)  # 0x00000002

    @property
    def is_library(self):
        """ Is a library function. """
        return bool(self.flags & idaapi.FUNC_LIB)  # 0x00000004

    @property
    def is_static(self):
        """ Is a static function. """
        return bool(self.flags & idaapi.FUNC_STATICDEF)  # 0x00000008

    @property
    def is_frame(self):
        """ Function uses frame pointer (BP) """
        return bool(self.flags & idaapi.FUNC_FRAME)  # 0x00000010

    @property
    def is_user_far(self):
        """ User has specified far-ness of the function. """
        return bool(self.flags & idaapi.FUNC_USERFAR)  # 0x00000020

    @property
    def is_hidden(self):
        """ A hidden function chunk. """
        return bool(self.flags & idaapi.FUNC_HIDDEN)  # 0x00000040

    @property
    def is_thunk(self):
        """ Thunk (jump) function. """
        return bool(self.flags & idaapi.FUNC_THUNK)  # 0x00000080

    @property
    def is_bottom_bp(self):
        """ BP points to the bottom of the stack frame. """
        return bool(self.flags & idaapi.FUNC_BOTTOMBP)  # 0x00000100

    @property
    def is_noret_pending(self):
        """ Function 'non-return' analysis must be performed. """
        return bool(self.flags & idaapi.FUNC_NORET_PENDING)  # 0x00200

    @property
    def is_sp_ready(self):
        """ SP-analysis has been performed. """
        return bool(self.flags & idaapi.FUNC_SP_READY)  # 0x00000400

    @property
    def is_purged_ok(self):
        """ 'argsize' field has been validated. """
        return bool(self.flags & idaapi.FUNC_PURGED_OK)  # 0x00004000

    @property
    def is_tail(self):
        """ This is a function tail. """
        return bool(self.flags & idaapi.FUNC_TAIL)  # 0x00008000


class Function(FunctionFlagsMixin):
    """IDA Function

    Provides easy access to function related APIs in IDA.
    """

    class UseCurrentAddress(object):
        """
        This is a filler object to replace `None` for the EA.
        In many cases, a programmer can accidentally initialize the
        `Function` object with `ea=None`, resulting in the current address.
        Usually, this is not the desired outcome. This object resolves this issue.
        """
        pass

    def __init__(self, ea=UseCurrentAddress, name=None):
        if name is not None and ea != self.UseCurrentAddress:
            raise ValueError(("Either supply a name or an address (ea). "
                              "Not both. (ea={!r}, name={!r})").format(ea, name))

        elif name is not None:
            ea = idc.LocByName(name)
            if ea == idc.BADADDR:
                raise exceptions.SarkNoFunction(
                    "The supplied name does not belong to an existing function. "
                    "(name = {!r})".format(name))

        elif ea == self.UseCurrentAddress:
            ea = idc.here()

        elif ea is None:
            raise ValueError("`None` is not a valid address. To use the current screen ea, "
                             "use `Function(ea=Function.UseCurrentAddress)` or supply no `ea`.")

        elif isinstance(ea, Line):
            ea = ea.ea
        self._func = get_func(ea)
        self._comments = Comments(self)

    @staticmethod
    def is_function(ea=UseCurrentAddress):
        try:
            Function(ea)
            return True
        except exceptions.SarkNoFunction:
            return False

    @staticmethod
    def create(ea=UseCurrentAddress):
        if ea == Function.UseCurrentAddress:
            ea = idc.here()

        if Function.is_function(ea):
            raise exceptions.SarkFunctionExists("Function already exists")

        if not add_func(ea):
            raise exceptions.SarkAddFunctionFailed("Failed to add function")

        return Function(ea)


    @property
    def comments(self):
        """Comments"""
        return self._comments

    def __eq__(self, other):
        try:
            return self.startEA == other.startEA
        except AttributeError:
            return False

    def __hash__(self):
        return self.startEA

    @property
    def lines(self):
        """Get all function lines."""
        return iter_function_lines(self._func)

    @property
    def startEA(self):
        """Start Address"""
        return self._func.startEA

    # Alias for `startEA` for increased guessability and less typing.
    ea = startEA

    @property
    def endEA(self):
        """End Address

        Note that taking all the lines between `startEA` and `endEA` does not guarantee
        that you get all the lines in the function. To get all the lines, use `.lines`.
        """
        return self._func.endEA

    @property
    def flags(self):
        """The function flags.

        See `idaapi.FUNC_*` constants.
        """
        return self._func.flags

    @property
    def xrefs_from(self):
        """Xrefs from the function.

        This includes the xrefs from every line in the function, as `Xref` objects.
        Xrefs are filtered to exclude code references that are internal to the function. This
        means that every xrefs to the function's code will NOT be returned (yet, references
        to the function's data will be returnd). To get those extra xrefs, you need to iterate
        the function's lines yourself.
        """
        for line in self.lines:
            for xref in line.xrefs_from:
                if xref.type.is_flow:
                    continue

                if xref.to in self and xref.iscode:
                    continue

                yield xref

    @property
    def calls_from(self):
        return (xref for xref in self.xrefs_from if xref.type.is_call)

    @property
    def drefs_from(self):
        """Destination addresses of data xrefs from this function."""
        for line in self.lines:
            for ea in line.drefs_from:
                yield ea

    @property
    def crefs_from(self):
        """Destination addresses of code xrefs from this function."""
        for line in self.lines:
            for ea in line.crefs_from:
                yield ea

    @property
    def xrefs_to(self):
        """Xrefs to the function.

        This only includes references to that function's start address.
        """
        return imap(Xref, idautils.XrefsTo(self.startEA))

    @property
    def drefs_to(self):
        """Source addresses of data xrefs to this function."""
        return idautils.DataRefsTo(self.startEA)

    @property
    def crefs_to(self):
        """Source addresses of code xrefs to this function."""
        return idautils.CodeRefsTo(self.startEA, 1)

    @property
    def name(self):
        """Function's Name"""
        return idaapi.get_ea_name(self.startEA)

    @property
    def demangled(self):
        """Return the demangled name of the function. If none exists, return `.name`"""
        return demangle(self.name)

    @name.setter
    def name(self, name):
        """Set the function name.

        If the name exists, an exception will be raised. To use IDA's name counting use
        `.set_name(desired_name, anyway=True)`.
        """
        self.set_name(name)

    def set_name(self, name, anyway=False):
        """Set Function Name.

        Default behavior throws an exception when setting to a name that already exists in
        the IDB. to make IDA automatically add a counter to the name (like in the GUI,)
        use `anyway=True`.

        Args:
            name: Desired name.
            anyway: `True` to set anyway.
        """
        set_name(self.startEA, name, anyway=anyway)

    def __repr__(self):
        return 'Function(name="{}", addr=0x{:08X})'.format(self.name, self.startEA)

    def __contains__(self, item):
        """Is an item contained (its EA is in) the function."""
        # If the item has an EA, use it. If not, use the item itself assuming it is an EA.
        ea = getattr(item, "ea", item)

        return is_same_function(ea, self.ea)

    @property
    def frame_size(self):
        return idaapi.get_frame_size(self._func)

    @property
    def color(self):
        """Function color in IDA View"""
        color = idc.GetColor(self.ea, idc.CIC_FUNC)
        if color == 0xFFFFFFFF:
            return None

        return color

    @color.setter
    @updates_ui
    def color(self, color):
        """Function Color in IDA View.

        Set color to `None` to clear the color.
        """
        if color is None:
            color = 0xFFFFFFFF

        idc.SetColor(self.ea, idc.CIC_FUNC, color)

    @property
    def has_name(self):
        return Line(self.startEA).has_name

    @property
    def func_t(self):
        return self._func

    @property
    def signature(self):
        '''The C signature of the function.'''
        return idc.GetType(self.startEA)

    @signature.setter
    def signature(self, c_signature):
        success = idc.SetType(self.startEA, c_signature)
        if not success:
            raise exceptions.SetTypeFailed(self.startEA, c_signature)

    @property
    def tinfo(self):
        '''The tinfo of the function type'''
        return idc.GetTinfo(self.startEA)

    @tinfo.setter
    def tinfo(self, tinfo):
        success = idc.ApplyType(self.startEA, tinfo)
        if not success:
            raise exceptions.SetTypeFailed(self.startEA, tinfo)


def iter_function_lines(func_ea):
    """Iterate the lines of a function.

    Args:
        func_ea (idaapi.func_t, int): The function to iterate.

    Returns:
        Iterator over all the lines of the function.
    """
    for line in idautils.FuncItems(get_ea(func_ea)):
        yield Line(line)


def functions(start=None, end=None):
    """Get all functions in range.

    Args:
        start: Start address of the range. Defaults to IDB start.
        end: End address of the range. Defaults to IDB end.

    Returns:
        This is a generator that iterates over all the functions in the IDB.
    """
    start, end = fix_addresses(start, end)

    for func_t in idautils.Functions(start, end):
        yield Function(func_t)
