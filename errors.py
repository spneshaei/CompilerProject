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
    
    def to_string(self, error):
        return "("+error['text']+", "+error['message']+") "

    def write_to_file(self):
        last_line_no = self.errors[0]['line_no'] if len(self.errors) > 0 else 0
        to_write = str(last_line_no) + ".\t"
        for error in self.errors:
            if error['line_no'] != last_line_no:
                to_write = to_write[:-1]
                to_write += "\n"
                to_write += str(error['line_no']) + ".\t"
                last_line_no = error['line_no']
            to_write += self.to_string(error)
        to_write = to_write[:-1]
        with open('lexical_errors.txt', 'w') as file:
            file.write(to_write)
            file.close()
