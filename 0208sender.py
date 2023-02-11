
btn = self.sender()

self.quize_name = btn.text()
if self.quize_name == '강원도':
    self.send_command('/quize_gangwon', self.quize_name)