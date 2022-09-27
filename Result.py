class Result:

    def create_result(self, file_names, output):
        with open(output, 'w') as f:
            for file_index in range(len(file_names)):
                file_name = r"{0}_{1}".format(file_index, output)
                print("reading file {0}".format(file_name))
                with open(file_name, 'r') as f1:
                    f.write(f1.read())
                    f.write('\n')

            print("result file created {}".format(output))
