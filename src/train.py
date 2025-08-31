import mlflow
import yaml
from ultralytics import YOLO
import os
from pathlib import Path
import matplotlib
matplotlib.use("Agg")

def main():


    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    params_path = PROJECT_ROOT / "params.yaml"
    try:
        with open(params_path,'r') as f:
            params = yaml.safe_load(f)['train']
    except Exception as e:
        print(f"error loading params.yaml1 : {e}")
        return
    
    os.environ['MLFLOW_EXPERIMENT_NAME'] = params['experiment_name']

    model = YOLO(params['model_version'])
    data_config_path = PROJECT_ROOT / params['data_config']

    print("Starting model training...")
    results = model.train(
        data=str(data_config_path),
        epochs=params['epochs'],
        batch=params['batch_size'],
        imgsz=params['img_Size'],
        project=str(PROJECT_ROOT / 'runs/detect'),
        name=params['run_name']
    )

    print("Model training complete.")
    print("\nMLflow run should be visible in the UI.")
    print(f"Trained model and outputs are in: {PROJECT_ROOT / 'runs/detect' / params['run_name']}")

if __name__ == "__main__":
    main()