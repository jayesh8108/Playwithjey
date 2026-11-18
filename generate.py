import argparse, json, subprocess, pathlib, textwrap
from PIL import Image, ImageDraw, ImageFont
ROOT=pathlib.Path(__file__).parent
font='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def run(*args): subprocess.run(args,check=True)
def main():
 p=argparse.ArgumentParser();p.add_argument('--format',choices=['short','long'],default='short');a=p.parse_args()
 data=json.loads((ROOT/'topics.json').read_text())[a.format]; out=ROOT/'output';out.mkdir(exist_ok=True)
 w,h=(720,1280) if a.format=='short' else (1280,720)
 segments=data['segments']; clips=[]
 for i,s in enumerate(segments):
  img=Image.new('RGB',(w,h),(13,13,22));d=ImageDraw.Draw(img)
  d.rectangle((0,0,w,20),fill=(235,35,58));d.text((45,50),'PLAYWITHJEY',font=ImageFont.truetype(font,35),fill='white')
  lines=textwrap.wrap(s['heading'],width=17 if a.format=='short' else 31)
  ft=ImageFont.truetype(font,57 if a.format=='short' else 66)
  y=h//3
  for line in lines:d.text((45,y),line,font=ft,fill=(255,255,255));y+=80
  d.text((45,h-100),'GTA 6  |  GAMING ANALYSIS',font=ImageFont.truetype(font,23),fill=(255,75,90))
  still=out/f'frame{i}.png';img.save(still)
  wav=out/f'voice{i}.wav';run('espeak-ng','-v','en-us','-s','145','-w',str(wav),s['narration'])
  clip=out/f'clip{i}.mp4';run('ffmpeg','-y','-loop','1','-framerate','25','-i',str(still),'-i',str(wav),'-c:v','libx264','-tune','stillimage','-c:a','aac','-b:a','128k','-pix_fmt','yuv420p','-shortest',str(clip));clips.append(clip)
 (out/'concat.txt').write_text(''.join("file '"+str(c.resolve())+"'\n" for c in clips))
 run('ffmpeg','-y','-f','concat','-safe','0','-i',str(out/'concat.txt'),'-c','copy',str(out / ('playwithjey_' + a.format + '.mp4')))
 thumb=Image.open(out/'frame0.png');thumb.save(out/'thumbnail_'+a.format+'.png')
 (out/'metadata.txt').write_text(data['title']+'\n\n'+data['description']+'\n')
 print('Created MP4, thumbnail and metadata in output/')
if __name__=='__main__':main()
