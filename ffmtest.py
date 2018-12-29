from subprocess import call

def export(duration, startx, starty, startz, endx, endy, endz):
  zoompan = f"zoompan=x='{startx}+({endx}-{startx})/zoom':y='{starty}+({endy}-{starty})/zoom':z='if(eq(on,1),{startz},zoom+({endz}-{startz})/(25*{duration}))':d='25*{duration}':s=1600*900"
  call(["ffmpeg", "-i", "testimg.png", "-i", "testsnd.mp3", "-filter_complex", zoompan, "testvid.flv"])

if __name__ == "__main__":
  d=14
  x0 = 0
  y0 = 60
  x1 = 60
  y1 = 0
  z0 = 3
  z1 = 2
  export(d,x0,y0,z0,x1,y1,z1)