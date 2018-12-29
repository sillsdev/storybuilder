from subprocess import call

d=14
x0 = 0
y0 = 60
x1 = 60
y1 = 0
z0 = 3
z1 = 2

zoompan = f"zoompan=x='{x0}+({x1}-{x0})/zoom':y='{y0}+({y1}-{y0})/zoom':z='if(eq(on,1),{z0},zoom+({z1}-{z0})/(25*{d}))':d='25*{d}':s=1600*900"

call(["ffmpeg", "-i", "testimg.png", "-i", "testsnd.mp3", "-filter_complex", zoompan, "testvid.flv"])