from flask import jsonify, session

# Check access to the pages
def check_access(flag):
    if 'user_id' in session and not flag:
        return jsonify({'message': 'You have already logged in. Log out to access to this page'}), 200
    elif not 'user_id' in session and flag:
        return jsonify({'message': 'You have already logged out. Log in to access to this page'}), 200
    else:
        return None