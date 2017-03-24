import pandas as pd

def read_surveys(codebook_file, data_file, key_in_header=0):
    with open(codebook_file) as test:
        questions = {}
        for line in test:
            if line.startswith('Q'):
                q_line = line.split('.')
                if len(q_line) <= 3:
                    questions[q_line[0]] = q_line[1]
                elif len(q_line) == 4:
                    divided_q1 = q_line[1].split('=')
                    divided_q2 = q_line[2].split('=')
                    questions[q_line[0]] = {divided_q1[0]: divided_q1[1], divided_q2[0]: divided_q2[1]}
                else:
                    questions[q_line[0]] = ".".join(q_line[1:-1])
    gender_key = {1: 'male', 2: 'female', 3: 'other', 0: 'none chosen'}
    survey_data = pd.read_csv(data_file)

    if key_in_header == 1:
        response_key = {1: 'strongly disagree', 2: 'disagree', 3: 'neutral', 4: 'agree', 5: 'strongly agree',
                        0: 'skipped'}
        return survey_data, questions, gender_key, response_key
    else:
        return survey_data, questions, gender_key