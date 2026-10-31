import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import edge_tts
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from starlette.background import BackgroundTask

ROOT = Path(__file__).parent
app = FastAPI(title='Capri Voice AI 2.0', version='2.0.0')
app.mount('/static', StaticFiles(directory=ROOT / 'static'), name='static')

class SpeechRequest(BaseModel):
    text: str = Field(min_length=1, max_length=1500)
    style: str = 'natural'
    speed: int = Field(default=0, ge=-30, le=30)

STYLES = {'natural': (0, '+0Hz'), 'cibernetica': (-5, '-2Hz')}

@app.get('/')
def home():
    return FileResponse(ROOT / 'static' / 'index.html')

@app.get('/health')
def health():
    return {'status': 'ok', 'version': '2.0.0'}

@app.post('/api/speak')
async def speak(req: SpeechRequest):
    if not req.text.strip():
        raise HTTPException(422, 'Texto vazio')
    if req.style not in STYLES:
        raise HTTPException(422, 'Estilo inválido')
    directory = tempfile.mkdtemp(prefix='capri_')
    source = os.path.join(directory, 'source.mp3')
    output = os.path.join(directory, 'output.mp3')
    try:
        base_rate, pitch = STYLES[req.style]
        rate = max(-50, min(50, base_rate + req.speed))
        await edge_tts.Communicate(req.text, voice='pt-BR-FranciscaNeural', rate=f'{rate:+d}%', pitch=pitch).save(source)
        if req.style == 'cibernetica':
            # Echo and gentle filtering; does not reproduce an actor's vocal identity.
            cmd = ['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-i', source,
                   '-af', 'highpass=f=110,lowpass=f=7500,aecho=0.8:0.28:65:0.16,alimiter=limit=0.92',
                   '-codec:a', 'libmp3lame', '-q:a', '3', output]
            subprocess.run(cmd, check=True, timeout=35, capture_output=True)
        else:
            shutil.copyfile(source, output)
        return FileResponse(output, media_type='audio/mpeg', filename=f'capri-{req.style}.mp3',
                            background=BackgroundTask(shutil.rmtree, directory, ignore_errors=True))
    except Exception as exc:
        shutil.rmtree(directory, ignore_errors=True)
        raise HTTPException(502, 'Não foi possível gerar áudio. Verifique a conexão do servidor e tente novamente.') from exc
