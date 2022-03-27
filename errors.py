class Errors:
    def __init__(self):
        self.errors = []

    def add_error(self, message, text, line_no):
        self.errors.append({
            "line_no": line_no,
            "text": text,
            "message": message,
        })

    # for debugging purposes only
    def print(self):
        for error in self.errors:
            print(error['line_no'], "(" + error['text'], ", " + error['message'] + ")")
