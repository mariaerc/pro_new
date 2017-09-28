import sys
import subprocess as spp

upName = sys.argv[1]
BASE5 = sys.argv[2]

spp.getstatusoutput("base64 -d "+BASE5+"v_"+upName+" >"+BASE5+upName)
#spp.getstatusoutput("rm -frv "+BASE6+upName)
#spp.getstatusoutput("ffmpeg -i "+BASE6+"v_"+upName+" -vcodec h264 -acodec aac -strict -2 "+BASE5+upName)
spp.getstatusoutput("rm -frv "+BASE5+"v_"+upName)
