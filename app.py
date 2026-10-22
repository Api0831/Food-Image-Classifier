from pathlib import Path

import streamlit as st
from PIL import Image, ImageOps, UnidentifiedImageError
import os

# Install dependencies explicitly, never during a prediction.
os.environ["YOLO_AUTOINSTALL"] = "false"
from ultralytics import YOLO

from labels import FOOD_LABELS_ZH


PROJECT_DIR = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_DIR / "models" / "food100.pt"


st.set_page_config(
    page_title="Food Image Classifier",
    page_icon="🍱",
    layout="centered",
)


@st.cache_resource(show_spinner="正在加载分类模型…")
def load_model(model_path: str) -> YOLO:
    """Load the model once per Streamlit server process."""
    return YOLO(model_path)


def label_for(class_name: str) -> str:
    """Return a Chinese label while preserving unknown model labels."""
    return FOOD_LABELS_ZH.get(class_name, class_name)


def predict(image: Image.Image) -> tuple[str, float, list[dict[str, object]]]:
    """Run one classification prediction and format the top-five results."""
    model = load_model(str(MODEL_PATH))
    result = model.predict(source=image, device="cpu", imgsz=128, verbose=False)[0]

    if result.probs is None:
        raise RuntimeError("The loaded model did not return classification probabilities.")

    class_names = result.names
    top_ids = result.probs.top5
    top_confidences = result.probs.top5conf.cpu().tolist()
    predictions = [
        {
            "类别": label_for(class_names[class_id]),
            "英文标签": class_names[class_id],
            "置信度": round(float(confidence) * 100, 2),
        }
        for class_id, confidence in zip(top_ids, top_confidences)
    ]

    best = predictions[0]
    return str(best["类别"]), float(best["置信度"]), predictions


st.title("🍱 Food Image Classifier")
st.caption("基于 YOLOv8 的 100 类日式食物图像分类演示")

with st.sidebar:
    st.header("项目说明")
    st.write("上传一张食物照片，模型会给出最可能的类别和 Top-5 预测。")
    st.caption("模型：YOLOv8s classification · 数据：UEC-FOOD100")
    st.info("仅识别训练集中的 100 类食物；非食物或未知类别也会得到预测。置信度不代表实际准确率。")

if not MODEL_PATH.exists():
    st.error("未找到模型文件：models/food100.pt")
    st.stop()

upload = st.file_uploader("上传食物图片", type=["jpg", "jpeg", "png"])

if upload is None:
    st.info("请选择一张 JPG 或 PNG 图片开始识别。")
    st.stop()

if upload.size > 10 * 1024 * 1024:
    st.error("图片不能超过 10 MB，请压缩后重试。")
    st.stop()

try:
    image = ImageOps.exif_transpose(Image.open(upload)).convert("RGB")
except (UnidentifiedImageError, OSError, Image.DecompressionBombError):
    st.error("无法读取该图片，请换一张 JPG 或 PNG 文件。")
    st.stop()

st.image(image, caption="待识别图片", width="stretch")

if st.button("开始分类", type="primary", width="stretch"):
    try:
        with st.spinner("正在分析图片…"):
            label, confidence, predictions = predict(image)
    except Exception as error:
        st.error(f"推理失败：{error}")
        st.stop()

    st.success(f"预测结果：{label}（{confidence:.2f}%）")
    st.subheader("Top-5 预测")
    st.dataframe(
        predictions,
        column_config={
            "置信度": st.column_config.ProgressColumn(
                "置信度 (%)", min_value=0, max_value=100, format="%.2f%%"
            )
        },
        hide_index=True,
        width="stretch",
    )
