# Laptop Price Predictor

Predicts laptop prices from RAM, storage, processor, graphics and other specs.
Built with scikit-learn (Ridge Regression and Random Forest) and Streamlit.

## Run locally
```
pip install -r requirements.txt
python make_dataset.py      # only if data/laptops.csv is missing
python train_model.py       # compare models
streamlit run app.py
```

## Dataset
`data/laptops.csv` columns: Brand, Ram_GB, Storage_GB, Storage_Type, Processor, GPU,
Screen_Size, Resolution, Price. The bundled file is synthetic demo data; replace it with a real dataset using the same columns.
