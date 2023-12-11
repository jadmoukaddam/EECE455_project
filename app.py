from flask import Flask, render_template, jsonify, request
from ECDSA import ECDSA
from ECC import ECC
from Point import Point
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def check_ECC_params(sign_data):
    try:
        sign_data['a']
        sign_data['b']
        sign_data['hash']
        sign_data['modulo']
        sign_data['basePointX']
        sign_data['basePointY']
    except:
        return False
    if not sign_data['a'] or int(sign_data['a'])<0:
        return False
    if not sign_data['b'] or int(sign_data['b'])<0:
        return False
    if not sign_data['hash'] or int(sign_data['hash'])<0:
        return False
    if not sign_data['modulo'] or int(sign_data['modulo'])<0:
        return False
    if not sign_data['basePointX'] or int(sign_data['basePointX'])<0:
        return False
    if not sign_data['basePointY'] or int(sign_data['basePointY'])<0:
        return False
    return True

def check_verify_params(sign_data):
    try:
        sign_data["r"]
        sign_data["s"]
        sign_data["publicKeyX"]
        sign_data["publicKeyY"]
    except:
        print("failing here")
        return False
    if not sign_data["r"] or int(sign_data["r"])<0:
        print("r")
        return False
    if not sign_data["s"] or int(sign_data["s"])<0:
        print("s")
        return False
    if not sign_data["publicKeyX"] or int(sign_data["publicKeyX"])<0:
        print("publicKeyX")
        return False
    if not sign_data["publicKeyY"] or int(sign_data["publicKeyY"])<0:
        print("publicKeyY")
        return False
    return True

@app.route('/api/sign', methods=['POST'])
def get_signature():
    print(request.get_json())
    if not check_ECC_params(request.get_json()):
        return jsonify({'error': 'Invalid parameters'}), 400
    modulo = int(request.get_json()['modulo'])
    a = int(request.get_json()['a'])
    b = int(request.get_json()['b'])
    basePointX = int(request.get_json()['basePointX'])
    basePointY = int(request.get_json()['basePointY'])
    try:
        curve = ECC(modulo, a, b, Point(basePointX, basePointY))
    except:
        return jsonify({'error': 'Invalid curve parameters, 4a^3 + 27b^2 mod n = 0 or G not on the curve'}), 400
    d = 1
    try:
        d = int(request.get_json()['d'])
        if d<1 or d>curve.order:
            return jsonify({'error': 'Invalid private key, should be between 1 and curve order - 1'}), 400
    except:
        d = ECDSA.generate_private_key(curve.order)
    k=-1
    ecdsa = ECDSA(curve, d)
    hash = int(request.get_json()['hash'])
    #if hash<0 or hash>curve.order:
    #    return jsonify({'error': 'Invalid hash, should be between 1 and curve order - 1'}), 400
    try:
        k = int(request.get_json()['k'])
        if k<0 or k>curve.order:
            return jsonify({'error': 'Invalid k, should be between 1 and curve order - 1'}), 400
    except:
        pass
    r,s = (-1,-1)
    if k==-1:
        try:
            r,s, k = ecdsa.sign(int(request.get_json()['hash']))
        except:
            return jsonify({'error': 'Could not generate k within 100 tries'}), 400
    else:
        try:
            r,s = ecdsa.sign(int(request.get_json()['hash']), k)
        except:
            return jsonify({'error': 'Invalid k, r=0, s=0 or s^-1 mod n does not exist'}), 400
    return jsonify({'r': r, 's': s, 'publicKeyX': ecdsa.get_public_key().x, 'publicKeyY': ecdsa.get_public_key().y, 'd' : d, 'k' : k}), 200

@app.route('/api/verify', methods=['POST'])
def verify_signature():
    if not check_ECC_params(request.get_json()):
        return jsonify({'error': 'Invalid curve parameters'}), 400
        
    if not check_verify_params(request.get_json()):
        return jsonify({'error': 'Invalid pubkey parameters or signature'}), 400
    modulo = int(request.get_json()['modulo'])
    a = int(request.get_json()['a'])
    b = int(request.get_json()['b'])
    basePointX = int(request.get_json()['basePointX'])
    basePointY = int(request.get_json()['basePointY'])
    curve = None
    try:
        curve = ECC(modulo, a, b, Point(basePointX, basePointY))
    except Exception as e:
        return jsonify({'error': 'Invalid curve parameters, 4a^3 + 27b^2 mod n = 0 or G not on the curve'}), 400

    r = int(request.get_json()['r'])
    s = int(request.get_json()['s'])
    publicKeyX = int(request.get_json()['publicKeyX'])
    publicKeyY = int(request.get_json()['publicKeyY'])
    Q = Point(publicKeyX, publicKeyY)
    ecdsa = ECDSA(curve, 1, Q=Q)
    hash = int(request.get_json()['hash'])
    #if hash<0 or hash>curve.order:
    #    return jsonify({'error': 'Invalid hash, should be between 1 and curve order - 1'}), 400
    verified = ecdsa.verify(int(request.get_json()['hash']), r, s)
    print("Got request: ", request.get_json())
    return jsonify({'verified': verified, 'publicKeyX' : publicKeyX, 'publicKeyY' : publicKeyY, 'r' : r, 's' : s, 'k' : ''}), 200


if __name__ == '__main__':
    app.run(debug=True)
