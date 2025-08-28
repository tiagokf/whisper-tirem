from flask import Flask, render_template, request, jsonify, send_file
from faster_whisper import WhisperModel
import os
import tempfile
import srt
from datetime import timedelta
from werkzeug.utils import secure_filename
import io
import zipfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB

# Modelo global
model = None
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'ogg', 'flac', 'aac', 'opus'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_whisper_model(model_size="small"):
    global model
    try:
        print(f"Carregando modelo {model_size}...")
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        print(f"Modelo {model_size} carregado com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao carregar modelo: {e}")
        return False

@app.route('/')
def index():
    print("Rota / acessada")
    return render_template('index.html')

@app.route('/health')
def health():
    return {'status': 'ok', 'model_loaded': model is not None}

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['audio']
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Formato de arquivo não suportado'}), 400
    
    # Parâmetros
    model_size = request.form.get('model_size', 'medium')
    language = request.form.get('language', 'auto')
    beam_size = int(request.form.get('beam_size', 5))
    
    # Carregar modelo se necessário
    if model is None or request.form.get('reload_model'):
        print(f"Carregando modelo {model_size} para transcrição...")
        if not load_whisper_model(model_size):
            return jsonify({'error': 'Erro ao carregar modelo'}), 500
    
    try:
        # Salvar arquivo temporário
        filename = secure_filename(file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp_file:
            file.save(tmp_file.name)
            audio_path = tmp_file.name
        
        # Transcrição
        lang_param = None if language == "auto" else language
        segments, info = model.transcribe(
            audio_path, 
            language=lang_param, 
            beam_size=beam_size,
            word_timestamps=True,
            vad_filter=True,
            vad_parameters=dict(
                min_silence_duration_ms=300,
                speech_pad_ms=400,
                max_speech_duration_s=float('inf')
            ),
            condition_on_previous_text=True,
            temperature=0.0,
            compression_ratio_threshold=2.4,
            log_prob_threshold=-1.0,
            no_speech_threshold=0.6
        )
        
        # Processar segmentos
        transcription_text = ""
        srt_content = []
        segments_data = []
        
        for i, segment in enumerate(segments, 1):
            start_time = timedelta(seconds=segment.start)
            end_time = timedelta(seconds=segment.end)
            text = segment.text.strip()
            
            transcription_text += text + " "
            srt_content.append(srt.Subtitle(
                index=i, 
                start=start_time, 
                end=end_time, 
                content=text
            ))
            
            segments_data.append({
                'start': str(start_time),
                'end': str(end_time),
                'text': text
            })
        
        # Gerar SRT
        srt_string = srt.compose(srt_content)
        
        # Limpar arquivo temporário
        os.unlink(audio_path)
        
        return jsonify({
            'success': True,
            'language': info.language,
            'confidence': f"{info.language_probability:.2%}",
            'transcription': transcription_text.strip(),
            'segments': segments_data,
            'srt': srt_string
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro na transcrição: {str(e)}'}), 500

@app.route('/download/<format>')
def download(format):
    text = request.args.get('text', '')
    srt_content = request.args.get('srt', '')
    filename = request.args.get('filename', 'transcription')
    
    if format == 'txt':
        return send_file(
            io.BytesIO(text.encode('utf-8')),
            as_attachment=True,
            download_name=f"{filename}.txt",
            mimetype='text/plain'
        )
    elif format == 'srt':
        return send_file(
            io.BytesIO(srt_content.encode('utf-8')),
            as_attachment=True,
            download_name=f"{filename}.srt",
            mimetype='text/srt'
        )

# Carregar modelo small na inicialização (melhor balanço)
print("Carregando modelo Whisper small...")
load_whisper_model("small")
print("Servidor Flask iniciado!")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Iniciando servidor na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)