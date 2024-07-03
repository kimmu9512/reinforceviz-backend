import os
from dotenv import load_dotenv
from app import create_app
load_dotenv()

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)

    {"iterations":{"0":{"0,0":{"best_action":"N","value":0.0},"0,1":{"best_action":"N","value":0.0},"0,2":{"best_action":"N","value":0.0},"1,0":{"best_action":"N","value":0.0},"1,2":{"best_action":"N","value":0.0},"2,0":{"best_action":"N","value":0.0},"2,1":{"best_action":"N","value":0.0},"2,2":{"best_action":"N","value":0.0},"3,0":{"best_action":"N","value":0.0},"3,1":{"best_action":"N","value":0.0},"3,2":{"best_action":"N","value":0.0}},"1":{"0,0":{"best_action":"N","value":0.0},"0,1":{"best_action":"N","value":0.0},"0,2":{"best_action":"N","value":0.0},"1,0":{"best_action":"N","value":0.0},"1,2":{"best_action":"N","value":0.0},"2,0":{"best_action":"N","value":0.0},"2,1":{"best_action":"N","value":0.0},"2,2":{"best_action":"N","value":0.0},"3,0":{"best_action":"N","value":0.0},"3,1":{"best_action":"Terminate","value":-1.0},"3,2":{"best_action":"Terminate","value":1.0}},"2":{"0,0":{"best_action":"N","value":0.0},"0,1":{"best_action":"N","value":0.0},"0,2":{"best_action":"N","value":0.0},"1,0":{"best_action":"N","value":0.0},"1,2":{"best_action":"N","value":0.0},"2,0":{"best_action":"N","value":0.0},"2,1":{"best_action":"W","value":0.0},"2,2":{"best_action":"E","value":0.7200000000000001},"3,0":{"best_action":"S","value":0.0},"3,1":{"best_action":"Terminate","value":-1.0},"3,2":{"best_action":"Terminate","value":1.0}}},"message":"Value Iteration completed"}