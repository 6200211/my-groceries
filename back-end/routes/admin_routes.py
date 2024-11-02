from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
def checkadmin(currentUser):
    from app import mongo
    user = mongo.db.users.find_one({'email': currentUser})
    print(user)
    if not user or not user.get('is_admin') == True:
        return False
    else: return True


adminRoutes = Blueprint('admin', __name__)

@adminRoutes.route('/admin/product', methods=['PUT'])
@jwt_required()
def addProduct():
    from app import mongo
    currentUser = get_jwt_identity()

    if checkadmin(currentUser) == False:
        return jsonify(message="Потрібні права адміністратора"), 403

    # Отримуємо деталі продукту з запиту
    name = request.json.get('name')
    price = request.json.get('price')
    quantity = request.json.get('quantity')
    category = request.json.get('category')
    description = request.json.get('description')

    # Перевірка обов'язкових полів
    if not name or not isinstance(price, (int, float)) or not isinstance(quantity, (int, float)) or not description:
        return jsonify(message="Помилка: некоректні дані"), 422

    # Додаємо продукт в базу даних
    mongo.db.products.insert_one({
        'name': name,
        'price': price,
        'quantity': quantity,
        'category': category,
        'description': description,
    })

    return jsonify(message="Продукт додано успішно"), 201

@adminRoutes.route('/admin/product', methods=['DELETE'])
@jwt_required()
def deleteProduct():
    from app import mongo
    currentUser = get_jwt_identity()

    if checkadmin(currentUser) == False:
        return jsonify(message="Потрібні права адміністратора"), 403

    # Отримуємо назву продукту з запиту
    productName = request.json.get('product name')

    # Перевірка наявності продукту
    product = mongo.db.products.find_one({'name': productName})
    if not product:
        return jsonify(message="Product not found."), 404

    # Видаляємо продукт з бази даних
    mongo.db.products.delete_one({'name': productName})

    return jsonify(message="Продукт видалено успішно."), 200

@adminRoutes.route('/admin/product', methods=['PUT'])
@jwt_required()
def editProduct():
    from app import mongo
    currentUser = get_jwt_identity()

    if checkadmin(currentUser) == False:
        return jsonify(message="Потрібні права адміністратора"), 403

    # Отримуємо дані для оновлення продукту
    productName = request.json.get('productName')
    updatedName = request.json.get('newName')
    updatedPrice = request.json.get('newPrice')
    updatedQuantity = request.json.get('newQuantity')
    updatedCategory = request.json.get('newCategory')
    updatedDescription = request.json.get('newDescription')

    # Перевірка наявності продукту
    product = mongo.db.products.find_one({'name': productName})
    if not product:
        return jsonify(message="Продукт не знайдено"), 404

    # Створюємо оновлені дані, які можуть бути змінені
    updateData = {}
    if updatedName:
        updateData['name'] = updatedName
    if updatedPrice is not None:
        updateData['price'] = updatedPrice
    if updatedQuantity is not None:
        updateData['quantity'] = updatedQuantity
    if updatedCategory:
        updateData['category'] = updatedCategory
    if updatedDescription:
        updateData['description'] = updatedDescription

    # Оновлюємо продукт в базі даних
    if updateData:
        mongo.db.products.update_one({'name': productName}, {'$set': updateData})

    return jsonify(message="Продукт оновлено успішно"), 200

@adminRoutes.route('/admin/getAllUsersNick', methods=['GET']) # Функція для виведення ніків та ID всіх користувачів
@jwt_required()
def getAllUsers():
    from app import mongo
    currentUser = get_jwt_identity()

    # Проверка прав администратора
    if not checkadmin(currentUser):
        return jsonify(message="Потрібні права адміністратора"), 403

    usersCursor = mongo.db.users.find({}, {"_id": 1, "username": 1})
    users = [{"_id": str(user["_id"]), "username": user.get("username", "No username")} for user in usersCursor]

    try:
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@adminRoutes.route('/admin/adminPanel', methods=['PUT']) #Функція для налаштування рівня доступа
@jwt_required()
def setUser():
    from app import mongo
    currentUser = get_jwt_identity()

    if not checkadmin(currentUser):
        return jsonify(message="Потрібні права адміністратора"), 403

    userID = request.json.get('user id')
    isadmin = request.json.get('is admin')
    isblocked = request.json.get('is blocked')
    isrunner = request.json.get('is runner')
    username = request.json.get('username')

    try:
        userID = ObjectId(userID)
    except:
        return jsonify(message="Невірний формат ID користувача"), 400

    user = mongo.db.users.find_one({"_id": userID, "username": username}, {"_id": 1})

    if user:

        result1 = mongo.db.users.update_one({'_id': userID}, {'$set': {'is_admin': bool(isadmin)}})
        result2 = mongo.db.users.update_one({'_id': userID}, {'$set': {'is_runner': bool(isrunner)}})
        result3 = mongo.db.users.update_one({'_id': userID}, {'$set': {'is_runner': bool(isblocked)}})
        if result1.modified_count > 0:
            return jsonify(message="Статус користувача оновлено (адмін)"), 200
        elif result2.modified_count > 0:
            return jsonify(message="Статус користувача оновлено (кур'єр)"), 200
        elif result3.modified_count > 0:
            return jsonify(message="Статус користувача оновлено (блок)"), 200
        else:
            return jsonify(message="Оновлень не відбулось"), 200
    else:
        return jsonify(message="Користувача не знайдено"), 404


@adminRoutes.route('/admin/adminPanel', methods=['GET']) #Функція для виведення списку адміністраторів
@jwt_required()
def getAdmins():
    from app import mongo
    currentUser = get_jwt_identity()

    if not checkadmin(currentUser):
        return jsonify(message="Потрібні права адміністратора"), 403

    usersAdminCursor = mongo.db.users.find({}, {"_id": 1, "username": 1, "is_admin": True})
    users = [{"_id": str(user["_id"]), "username": user.get("username", "No username")} for user in usersAdminCursor]

    try:
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@adminRoutes.route('/admin/adminPanelRunners', methods=['GET'])#Функція для виведення списку кур'єрів
@jwt_required()
def getRunners():
    from app import mongo
    currentUser = get_jwt_identity()

    if not checkadmin(currentUser):
        return jsonify(message="Потрібні права адміністратора"), 403

    usersRunnersCursor = mongo.db.users.find({"is_runner": True},{})
    users = [{"_id": str(user["_id"]), "username": user.get("username", "No username")} for user in usersRunnersCursor]
    try:
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@adminRoutes.route('/admin/adminPanel', methods=['DELETE'])#Функція для видалення користувача
@jwt_required()
def delAdmins():
    from app import mongo
    currentUser = get_jwt_identity()

    if not checkadmin(currentUser):
        return jsonify(message="Потрібні права адміністратора"), 403

    userID = request.json.get('user id')
    username = request.json.get('username')

    try:
        userID = ObjectId(userID)
    except:
        return jsonify(message="Невірний формат ID користувача"), 400

    if mongo.db.users.find_one({"_id": userID, "username": username}, {"_id": 1}):
        mongo.db.users.delete_one({'_id': userID})
        return jsonify("Користувача видалено успішно"), 200
    else:
        return jsonify("Помилка видалення користувача"), 500

@adminRoutes.route('/admin/adminPanelBlocked', methods=['GET']) #Функція для перегляду заблокованих користувачів
@jwt_required()
def getBlocked():
    from app import mongo
    currentUser = get_jwt_identity()

    if not checkadmin(currentUser):
        return jsonify(message="Потрібні права адміністратора"), 403

    usersRunnersCursor = mongo.db.users.find({"is_blocked": True},{})
    users = [{"_id": str(user["_id"]), "username": user.get("username", "No username")} for user in usersRunnersCursor]
    try:
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500