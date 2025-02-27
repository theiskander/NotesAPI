from flask import jsonify, session

# Check access to the pages
def check_access(flag):
    if 'user_id' in session and not flag:
        return jsonify({'message': 'Log out to access to this page'}), 200
    elif not 'user_id' in session and flag:
        return jsonify({'message': 'Log in to access to this page'}), 200
    else:
        return None

# Check user id
def check_user(item):
    if item.user_id != session['user_id']:
        return jsonify({'message': 'You can only work with your items'}), 200
    
    return None