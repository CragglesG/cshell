from shell_extensions import ShellExtension

class TestExtension(ShellExtension):
    def __init__(self):
        super().__init__("test-extension", self.test)
    
    def test(self, msg, pathfiles, builtins):
        return ["This is a test extension\n"]