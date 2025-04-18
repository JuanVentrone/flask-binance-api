#  app.py (Flask API que usa get_data desde apiBinance.py con username opcional)
from flask import Flask, request, jsonify
from apiBinance import get_data

app = Flask(__name__)
@app.route('/api/workers', methods=['GET'])
def handle_workers():
    username = request.args.get('username', default='crislalo6vic')
    limit = request.args.get('limit', default=100, type=int)
    page = request.args.get('page', default=None, type=int)

    try:
        data = get_data(username, limit, page)  # nuevo arg `page`
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
