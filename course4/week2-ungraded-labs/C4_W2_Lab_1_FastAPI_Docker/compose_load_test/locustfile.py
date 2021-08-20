from locust import HttpUser, task, constant


class LoadTest(HttpUser):
    wait_time = constant(0)
    host = "http://localhost"

    @task
    def predict_batch_1(self):
        request_body = {"batches": [[1.0 for i in range(13)]]}
        self.client.post(
            "http://batch-1:80/predict", json=request_body, name="batch-1"
        )

    @task
    def predict_batch_32(self):
        request_body = {"batches": [[1.0 for i in range(13)] for i in range(32)]}
        self.client.post(
            "http://batch-32:80/predict", json=request_body, name="batch-32"
        )

    @task
    def predict_batch_64(self):
        request_body = {"batches": [[1.0 for i in range(13)] for i in range(64)]}
        self.client.post(
            "http://batch-64:80/predict", json=request_body, name="batch-64"
        )

    @task
    def predict_no_batch(self):
        request_body = {
            "alcohol": 1.0,
            "malic_acid": 1.0,
            "ash": 1.0,
            "alcalinity_of_ash": 1.0,
            "magnesium": 1.0,
            "total_phenols": 1.0,
            "flavanoids": 1.0,
            "nonflavanoid_phenols": 1.0,
            "proanthocyanins": 1.0,
            "color_intensity": 1.0,
            "hue": 1.0,
            "od280_od315_of_diluted_wines": 1.0,
            "proline": 1.0,
        }
        self.client.post(
            "http://no-batch:80/predict", json=request_body, name="0:batch"
        )
