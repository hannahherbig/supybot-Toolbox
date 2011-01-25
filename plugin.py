###
# Copyright (c) 2010, Andrew Herbig
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import os
import time

class Toolbox(callbacks.Plugin):
    """Add the help for "@plugin help Toolbox" here
    This should describe *how* to use this plugin."""
    threaded = True
    def pisg(self, irc, msg, args):
        irc.reply('Starting pisg (perl IRC statistics generator)...')
        channel = msg.args[0].lower()
        starttime = time.time()
        try: os.mkdir('pisg_cache')
        except: pass
        try: os.makedirs(os.path.join('/home/andrew/public_html/stats/', irc.network, channel[1:]))
        except: pass
        fd = open('pisg.cfg', 'w')
        fd.write("""
        <include="/home/andrew/pisg-include.cfg">

        <channel="%s">
            Logfile="%s"
            Format="supy"
            Network="%s"
            OutputFile="%s"
        </channel>
""" % (channel, os.path.join('/home/andrew/supybot/logs/ChannelLogger', irc.network, channel, '*.log'), irc.network, 
os.path.join('/home/andrew/public_html/stats/', 
irc.network, channel[1:], 'index.html')))
        fd.close()
        os.system('~/pisg-0.72/pisg')
        irc.reply('pisg update finished in %s seconds.' % (time.time() - starttime), prefixNick=False)
        irc.reply('http://matrix.mcintec.net/~andrew/stats/%s/%s/' % (irc.network, channel[1:]), prefixNick=False)
    pisg = wrap(pisg)

Class = Toolbox
