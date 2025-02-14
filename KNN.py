
#import thư viện cần thiết
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from matplotlib.pyplot import show
from imutils import paths
import pickle
import pickle


from datasets.simpledatasetloader import SimpleDatasetLoader
from preprocessing.simplepreprocessor import SimplePreprocessor


print("[INFO] Nạp ảnh để train...")
imagePaths = list(paths.list_images("datasets/animals"))


sp = SimplePreprocessor(32, 32)
sdl = SimpleDatasetLoader(preprocessors=[sp])
(data, labels) = sdl.load(imagePaths, verbose=500)
data = data.reshape((data.shape[0], 3072))

print("[INFO] Dung lượng Ma trận đặc trưng: {:.1f}MB".format(data.nbytes / (1024 * 1000.0)))

le = LabelEncoder()
labels = le.fit_transform(labels)

(trainData, testData, trainLabel, testLabel) = train_test_split(data, labels, test_size=0.25, random_state=42)

print("[Đánh giá Bộ phân lớp k-NN ...]")
model = KNeighborsClassifier(n_neighbors=3, n_jobs=-1)
model.fit(trainData, trainLabel)
# Tải mô hình từ tệp
with open('knnpickle_file.pkl', 'rb') as file:
    knn_model = pickle.load(file)

# Sử dụng mô hình để dự đoán
predictions = knn_model.predict(new_data)

# Lưu file model
knnPickle = open('knnpickle_file.pkl', 'wb')
pickle.dump(model, knnPickle)

print(classification_report(testLabel, model.predict(testData), target_names=le.classes_))

# Tạo và hiển thị ma trận confusion
cm = confusion_matrix(testLabel, model.predict(testData))
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
show()