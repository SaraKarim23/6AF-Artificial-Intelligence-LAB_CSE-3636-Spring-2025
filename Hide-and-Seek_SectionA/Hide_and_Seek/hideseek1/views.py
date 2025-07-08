from cProfile import Profile
import os
from django.shortcuts import render,HttpResponse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from requests import request
from hideseek1.models import Profile
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import io
import base64
import re



import emoji
from better_profanity import profanity
from nltk.corpus import words as nltk_words
import nltk
# Create your views here.
def Index(request):
    return render(request, 'Index.html')
def regsuc(request):
    return render(request, 'regsuc.html')
def wruser(request):
    return render(request, 'wruser.html')
def wremail(request):
    return render(request, 'wremail.html')
def wrconpass(request):
    return render(request, 'wremail.html')
def loginunsuc(request):
    return render(request, 'loginunsuc.html')
def notsignup(request):
    return render(request, 'notsignup.html')
def DIP(request):
    return render(request, 'DIP.html')
def NIU(request):
    return render(request, 'NIU.html')
def PCP(request):
    return render(request, 'PCP.html')
def NPCP(request):
    return render(request, 'NPCP.html')
def NS(request):
    return render(request, 'NS.html')
def NEI(request):
    return render(request, 'NEI.html')
def UEM(request):
    return render(request, 'UEM.html')
def About(request):
    return render(request, 'About.html')
def Gallery1(request):
    return render(request, 'Gallery1.html')
def Gallery2(request):
    return render(request, 'Gallery2.html')
def Home(request):
    return render(request, 'Home.html')
def encode(request):
    if request.method == 'POST':
        photo = request.FILES.get('photo')
        secretmsg = request.POST.get('secretmsg')
        password = request.POST.get('pass')
        confirm_password = request.POST.get('cpass')

        if not photo:
            return render(request, 'NIU.html', {'error_message': 'No photo provided'})
        if not password or not confirm_password:
            return render(request, 'NPCP.html')
        if password != confirm_password:
            return render(request, 'PCP.html')
        if not secretmsg:
            return render(request, 'NS.html')
        if not is_message_valid(secretmsg):
            return render(request, 'UEM.html', {
                'unsafe_message': secretmsg,  # Pass the actual unsafe message here
            })



        image = Image.open(photo)
        encoded_image = encode_message(image, secretmsg, password)

        # Save to memory
        encoded_image_file = BytesIO()
        encoded_image.save(encoded_image_file, format='PNG')
        encoded_image_file.seek(0)
        encoded_image_base64 = base64.b64encode(encoded_image_file.getvalue()).decode('utf-8')

        request.session['encoded_image_base64'] = encoded_image_base64
        return render(request, 'Home.html', {'encoded_photo': True})

    return render(request, 'Home.html')


# ========== DECODING VIEW ==========

def decode(request):
    if request.method == 'POST':
        photo = request.FILES.get('photo')
        password = request.POST.get('pass')

        if not photo:
            return render(request, 'NIU.html')
        if not password:
            return render(request, 'NPCP.html')

        try:
            image = Image.open(photo)
            decoded_message = decode_message(image, password)
            return render(request, 'Home.html', {'decoded_message': decoded_message})
        except ValueError as e:
            return render(request, 'DIP.html', {'error': str(e)})
        except Exception:
            return render(request, 'NEI.html')  # corrupted/invalid image

    return render(request, 'Home.html')


# ========== DOWNLOAD VIEW ==========

def download(request, filename):
    encoded_image_base64 = request.session.get('encoded_image_base64')
    if encoded_image_base64:
        encoded_image_data = base64.b64decode(encoded_image_base64)
        encoded_image_io = BytesIO(encoded_image_data)
        encoded_image = Image.open(encoded_image_io)

        temp_filename = "temp.png"
        encoded_image.save(temp_filename, format='PNG')
        with open(temp_filename, 'rb') as file:
            file_data = file.read()

        response = HttpResponse(file_data, content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        os.remove(temp_filename)
        return response
    else:
        return render(request, 'NEI.html')


# ========== HELPER: ENCODE MESSAGE WITH PASSWORD & LENGTH ==========

def encode_message(image, message, password):
    msg_bytes = message.encode('utf-8')
    pwd_bytes = password.encode('utf-8')

    if len(pwd_bytes) > 255:
        raise ValueError("Password too long. Must be under 255 characters.")

    data = bytearray()
    data.append(len(pwd_bytes))                  # 1 byte: password length
    data.extend(pwd_bytes)                       # N bytes: password
    data.extend(len(msg_bytes).to_bytes(4, 'big'))  # 4 bytes: message length
    data.extend(msg_bytes)                       # M bytes: message

    bits = ''.join(format(byte, '08b') for byte in data)

    if len(bits) > image.width * image.height * 3:
        raise ValueError("Data too large for image.")

    encoded_image = image.copy()
    bit_index = 0

    for y in range(encoded_image.height):
        for x in range(encoded_image.width):
            pixel = list(encoded_image.getpixel((x, y)))
            for i in range(3):
                if bit_index < len(bits):
                    pixel[i] = (pixel[i] & 0xFE) | int(bits[bit_index])
                    bit_index += 1
            encoded_image.putpixel((x, y), tuple(pixel))
            if bit_index >= len(bits):
                break
        if bit_index >= len(bits):
            break

    return encoded_image


# ========== HELPER: DECODE MESSAGE WITH PASSWORD CHECK ==========

def decode_message(image, input_password):
    bits = ''
    for y in range(image.height):
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            for i in range(3):
                bits += str(pixel[i] & 1)

    # Convert bits to bytes
    bytes_data = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        if len(byte) < 8:
            break
        bytes_data.append(int(byte, 2))

    # Parse password length
    pwd_len = bytes_data[0]
    if len(bytes_data) < 1 + pwd_len + 4:
        raise ValueError("Corrupted image or incomplete data")

    pwd_encoded = bytes_data[1:1 + pwd_len]
    actual_password = pwd_encoded.decode('utf-8', errors='replace')

    if actual_password != input_password:
        raise ValueError("Invalid password")

    msg_len_bytes = bytes_data[1 + pwd_len:1 + pwd_len + 4]
    msg_len = int.from_bytes(msg_len_bytes, 'big')

    msg_start = 1 + pwd_len + 4
    msg_end = msg_start + msg_len

    if msg_end > len(bytes_data):
        raise ValueError("Message length exceeds data capacity")

    msg_bytes = bytes_data[msg_start:msg_end]
    decoded_msg = msg_bytes.decode('utf-8', errors='replace')

    return decoded_msg
    
def Changepassword(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            # Handle form submission
            current_password = request.POST.get('cpassword')
            new_password = request.POST.get('npassword')
            confirm_password = request.POST.get('conpassword')

            # Perform password validation
            if not request.user.check_password(current_password):
                return render(request, 'incpass.html')
            elif new_password != confirm_password:
                return render(request, 'wpass.html')
            elif new_password == current_password:
                return render(request, 'samepass.html')
            else:
                # Update the password
                user = request.user
                user.set_password(new_password)
                user.save()

                # Keep the user logged in
                update_session_auth_hash(request, user)

                return render(request, 'successpass.html')
    return render(request, 'Changepassword.html')
def samepass(request):
    return render(request, 'samepass.html')
def wpass(request):
    return render(request, 'wpass.html')
def incpass(request):
    return render(request, 'incpass.html')
def successpass(request):
    return render(request, 'successpass.html')
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user)
            return render(request, 'Home.html')
            #return HttpResponse('Success')
        else:
            # Check if the username exists in the system
            if User.objects.filter(username=username).exists():
                # Username exists but password is incorrect
                return render(request, 'loginunsuc.html')
                #return HttpResponse('Invalid login credentials')
            else:
                # Redirect to signup page if username doesn't exist
                return render(request, 'notsignup.html') # Replace 'signup' with the actual URL name for the signup page

    return render(request, 'login.html')


def handleSignup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpass')
        profile_photo = request.FILES.get('photo')  # Get the profile photo file

        if password != confirmpassword:
            return render(request, 'wrconpass.html')

        try:
            if User.objects.get(email=email):
                return render(request, 'wremail.html')
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(username=username):
                return render(request, 'wruser.html')
        except User.DoesNotExist:
            pass

        myuser = User.objects.create_user(username=username, email=email, password=password)
        
        try:
            profile = Profile.objects.get(user=myuser)
        except ObjectDoesNotExist:
            profile = Profile(user=myuser)
        
        profile.photo = profile_photo  # Save the profile photo to the user's profile
        profile.save()
        myuser.save()

        return render(request, 'regsuc.html')
    else:
        return render(request, 'Signup.html')


# Ensure the English word list is loaded (required for initial setup)

try:
    ENGLISH_DICTIONARY = set(nltk_words.words())
except LookupError:
    nltk.download('words')
    ENGLISH_DICTIONARY = set(nltk_words.words())

# Load default profane words
profanity.load_censor_words()

HATE_PHRASES = ['i hate you', 'you are stupid', 'go to hell', 'you should die', 'kill yourself']

BANNED_WORDS = ['kill', 'hate', 'bomb', 'attack', 'terror', 'bombing', 'terrorist', 'gun', 'hijack', 'explosion', 'assault']

# Constraint check functions

def check_message_length(message):
    max_len = 5000
    if len(message) <= max_len:
        return True, f"OK: {len(message)}/{max_len} characters."
    return False, f"Too long: {len(message)} chars."


def check_profanity(message):
    profane_words_found = []

    # Use regex to extract all words (ignores punctuation)
    words = re.findall(r"\b\w+\b", message.lower())

    for word in words:
        if profanity.contains_profanity(word):
            profane_words_found.append(word)

    if profane_words_found:
        unique_detected = sorted(set(profane_words_found))
        return False, f"Contains profane words: {', '.join(unique_detected)}"

    return True, "No profanity."


def check_banned_words(message):
    print("[DEBUG] Running check_banned_words")
    message_words = re.findall(r"\b\w+\b", message.lower())
    found = [w for w in message_words if w in BANNED_WORDS]
    if found:
        return False, f"Banned words found: {', '.join(sorted(set(found)))}"
    return True, "No banned words detected"



def check_hate_speech(message):
    for phrase in HATE_PHRASES:
        if phrase in message.lower():
            return False, f"Hate speech detected: '{phrase}'"
    return True, "No hate speech detected"

def check_emoji_unicode(message):
    if emoji.emoji_count(message) > 0:
        return False, "Emoji detected."
    if any(ord(ch) > 127 for ch in message):
        return False, "Non‑ASCII Unicode detected."
    return True, "No emoji/Unicode."

def check_binary_like(message):
    if re.fullmatch(r"[01\s]+", message.strip()):
        return False, "Binary‑like content."
    return True, "Not binary."

def check_all_caps(message):
    letters = re.findall(r"[A-Za-z]", message)
    if letters and all(ch.isupper() for ch in letters):
        return False, "All letters are uppercase."
    return True, "Mixed case or lowercase present."

def check_punctuation(message):
    if any(p in message for p in ".?!"):
        return True, "Punctuation found."
    return False, "Missing punctuation."

def check_dictionary_presence(message):
    words_list = re.findall(r"\b\w+\b", message.lower())
    if not words_list:
        return False, "No words found."
    recognized = sum(1 for w in words_list if w in ENGLISH_DICTIONARY)
    ratio = recognized / len(words_list)
    if ratio < 0.4:
        return False, f"Dictionary match low ({ratio:.0%})."
    return True, f"Dictionary match ok ({ratio:.0%})."

def message_validator_view(request):
    results = []
    overall_safe = True
    message = ""

    # Prefer POST data, fallback to GET parameter 'message'
    if request.method == "POST":
        message = request.POST.get("message", "")
    else:
        message = request.GET.get("message", "")

    if message:
        checks = [
            ("Message Length", check_message_length),
            ("Profanity", check_profanity),
            ("Banned Words", check_banned_words),
            ("Hate Speech / Toxicity", check_hate_speech),
            ("Emoji / Unicode", check_emoji_unicode),
            ("Binary-like Content", check_binary_like),
            ("All CAPS Check", check_all_caps),
            ("Punctuation Check", check_punctuation),
            ("Dictionary Presence", check_dictionary_presence),
        ]

        for name, fn in checks:
            status, reason = fn(message)
            results.append({"check": name, "status": status, "reason": reason})
            overall_safe &= status

    return render(request, "message_validator.html", {
        "results": results,
        "overall_safe": overall_safe,
        "message": message,
    })


def is_message_valid(message):
    checks = [
        check_message_length,
        check_profanity,
        check_banned_words,
        check_hate_speech,
        check_emoji_unicode,
        check_binary_like,
        check_all_caps,
        check_punctuation,
        check_dictionary_presence,
    ]

    for check_fn in checks:
        status, _ = check_fn(message)
        if not status:
            return False
    return True


