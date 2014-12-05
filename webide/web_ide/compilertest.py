from ideone import Ideone
# interface with ideone compiler
# http://ideone.com/sphere-engine

class WebCompiler:

    user = "lne1"
    password = "eecs393"
    i = Ideone(user, password)

    def __init__(self):
        pass

    def run_code(self, src):
        sub = self.submit_code(src)
        link = sub['link']
        sub_info = self.submission_info(link)
        error = self.get_error(sub_info)
        output = self.get_output(sub_info)
        if error != 'OK':
            return error + output
        else: return output


    def test_response(self):
        return self.i.test()

    def submit_code(self, src):
        #src should be a string representation of the source code
        #returns a  list with error message and link code used to get the output
        #example return: { 'error':'OK', 'link':'LsSbo'}
        return self.i.create_submission(src, language_name='Java')

    def submission_info(self, link):
        ''' {'cmpinfo': "",
        'date': "2011-04-18 15:24:14",
        'error': "OK",
        'input': "",
        'langId': 116,
        'langName': "Python 3",
        'langVersion': "python-3.1.2",
        'memory': 5852,
        'output': 42,
        'public': True,
        'result': 15,
        'signal': 0,
        'source': "print(42)",
        'status': 0,
        'stderr': "",
        'time': 0.02}'''
        return self.i.submission_details(link)

    def get_date(self, sub_info):
        return sub_info['date']

    def get_error(self, sub_info):
        return sub_info['error']

    def get_output(self, sub_info):
        return sub_info['output']












