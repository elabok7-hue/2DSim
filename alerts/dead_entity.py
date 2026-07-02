from alerts.alert import Alert


class DeadEntityAlert(Alert):
    def update(self, data):
        print(f" No {data["entity"]}s remain alive!")
