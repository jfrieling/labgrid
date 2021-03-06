from pexpect import TIMEOUT

from ..util import PtxExpect
from ..step import step
from .common import Driver


class ConsoleExpectMixin:
    """
    Console driver mixin to implement the read, write, expect and sendline methods. It uses
    the internal _read and _write methods. 
    """

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._expect = PtxExpect(self)

    @Driver.check_active
    def read(self):
        return self._read()

    @Driver.check_active
    def write(self, data):
        self._write(data)

    @Driver.check_active
    def sendline(self, line):
        self._expect.sendline(line)

    @Driver.check_active
    def sendcontrol(self, char):
        self._expect.sendcontrol(char)

    @Driver.check_active
    @step(args=['pattern'], result=True)
    def expect(self, pattern, timeout=-1):
        index = self._expect.expect(pattern, timeout=timeout)
        return index, self._expect.before, self._expect.match, self._expect.after

    def resolve_conflicts(self, client):
        for other in self.clients:
            if other is client:
                continue
            self.target.deactivate(other)
