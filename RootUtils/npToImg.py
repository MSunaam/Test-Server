from PIL import Image
import base64
import io

def npToImg64(npArray):
    noiseImg = Image.fromarray(npArray)
    noise_byte_array = io.BytesIO()
    noiseImg.save(noise_byte_array, format='PNG')
    noise_byte_array.seek(0)

    return f"data:image/png;base64,{base64.b64encode(noise_byte_array.read()).decode('utf-8')}"