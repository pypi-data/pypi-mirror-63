# ############################################################################
# |L|I|C|E|N|S|E|L|I|C|E|N|S|E|L|I|C|E|N|S|E|L|I|C|E|N|S|E|
# Copyright (c) Bertrand Nouvel.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the University nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
# |P|R|O|G|R|A|M|P|R|O|G|R|A|M|P|R|O|G|R|A|M|P|R|O|G|R|A|M|
# ############################################################################

import os


## ---------------------------------------------------------------------------------------------------
##
## This manage the state of the screen
## For instance, we may want to render offscreen with audio for cast via chromecost or other fancy stuffs.
## Alternatively we may want to ensure that current screen is on and usable (dpms, etc...)
## or we may want to ensure that a specific window is displayed in a specific way on the screen
## and this may require setup/
##
## ---------------------------------------------------------------------------------------------------


class OffscreenRendering:
    """
    Provides offscreen rendering via nested X
    """
    def __init__(self, command="molotov", display=":7", audiochannel="cc-ramble"):
        self.command = command
        self.p = []
        self.cp = None

        self.display = display
        self.cc1 = audiochannel
        self.env = {k: v for k, v in os.environ.items()}
        self.env.update({
            "DISPLAY": self.display,
            "PULSE_SYNC": self.cc1,
        })

    async def __aenter__(self):
        #        self.p.append( subprocess.Popen("Xnest "+self.display, shell=True))
        self.p.append(subprocess.Popen("Xephyr -screen 1920x1080 " + self.display, shell=True))
        self.cp = subprocess.Popen(
            "pactl load-module module-null-sink sink_name=%s sink_properties=device.description=\"%s\"" % (self.cc1,
                                                                                                           self.cc1),
            shell=True
        )

        self.p.append(subprocess.Popen(
            "[ -f ~/.config/i3/config] || i3-config-wizard ; i3",
            shell=True,
            env=self.env
        ))

        self.p.append(subprocess.Popen(
            self.command,
            shell=True,
            env=self.env
        )
        )

        # self.p4 = subprocess.Popen(
        #     entry.get("command", "konsole"),
        #     shell=True,
        #     env=env
        # )

    def tick(self):
        for i, p in list(enumerate(self.p))[::-1]:
            if p.returncode is None:
                p.poll()
            if p.returncode is not None:
                p.wait()
                del self.p[i]
        self.p = []

    async def __aexit__(self):
        self.tick()
        for i, p in list(enumerate(self.p)):
            os.kill(self.p[i], 9)
        self.tick()
        os.system(
            "for m in $(pactl list modules | grep '" + cc1 + "' -B 3 | grep Module | cut -d '#' -f 2 | tr '\n' ' '); do pactl unload-module $m; done"
        )

        # await self.play_via_vlc({"url": "screen://"},
        #                         extra_opts=f"--input-slave pulse://{cc1}.monitor",
        #                         env=env
        #                         )
        #


class ActivescreenRendering:
    def __init__(self):
        pass

    async def __aenter__(self):
        os.system("xset s noblank")
        os.system("xset s off")
        os.system("xset dpms force on")
        os.system("xset -dpms")

    async def __aexit__(self, *args):
        os.system("xset +dpms")
        os.system("xset s on")

        #org.kde.kscreen.osdService
        # showOsd

