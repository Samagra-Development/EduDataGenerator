import numpy as np
import pandas as pd
import random as rnd

# data about the school
school_df = pd.read_csv('./SchoolTable.csv')

ID_START = 0

def generate_data(num_row,subjects,cl=12):
    assesments = np.array(['SA-1','SA-2','FA-1','FA-2','FA-3','FA-4'])
    num_subject = len(subjects)
    global ID_START
    # set assesment for each subject
    subjects = np.repeat(subjects,len(assesments)).reshape(-1,1)
    assesments = np.tile(assesments,num_subject).reshape(-1,1)
    
    # subject along with assestment
    subjects_info = np.hstack([subjects,assesments])
    
    #----SPECIFIC STUDENT RELATED INFORMATION----#
    # adding student info
    student_id = np.arange(1,num_row+1) + 1_00_00_000 + ID_START
    student_rollnumber = np.arange(1,num_row+1) + 1_02_00_00_000 + ID_START
    ID_START += num_row
    if cl==3:
        grade = np.random.randint(1,4,size=num_row)
    else:
        grade = np.random.randint(4,13,size=num_row)
    student_info = np.hstack([student_id.reshape(-1,1),student_rollnumber.reshape(-1,1),grade.reshape(-1,1)])
    
    # adding school info
    school_data = school_df[['Schoolcode','District','Block','Cluster']].values
    np.random.shuffle(school_data)
    
    num_times_to_repeat_class = num_row//len(school_data) + 1
    student_schools = np.vstack([school_data]*num_times_to_repeat_class)[:num_row,:]
    np.random.shuffle(student_schools)
    
    # concatentaing student school with 
    student_complete_info = np.hstack([student_schools,student_info])
    
    # repeat student for each subject
    sub_repeated = np.vstack([subjects_info]*num_row)
    student_repeated = np.repeat(student_complete_info,len(subjects_info),0)
    
    # concatenate them to generate final data
    data = np.hstack([student_repeated,sub_repeated])
    
    return data

def get_marks(df):
    # for marks obtained
    total_assesments = len(df)

    # 10% of total is for <=33
    per_10 = total_assesments//10
    marks_33 = np.random.randint(0,34,per_10)
    # 10% for greater >=90
    marks_100 = np.random.randint(90,101,per_10)
    # rest for between 
    per_80 = total_assesments - 2*per_10
    marks_90 = np.random.randint(34,90,per_80)

    # join all the marks
    marks = np.concatenate([marks_100,marks_33,marks_90])

    #shuffle the marks
    np.random.shuffle(marks)
    
    return marks

def save_df(iter_number):
    # Total number of students to generate
    NUM_STUDENTS = 1_00_000

    NUM_LESS_THEN_CLASS_3 = (NUM_STUDENTS//12)*3
    NUM_GREATER_THEN_CLASS_3 = NUM_STUDENTS - NUM_LESS_THEN_CLASS_3
    # generate < class 3 data
    data_3 = generate_data(NUM_LESS_THEN_CLASS_3,['HINDI','ENGLISH','MATHS'],3)
    # generate > class 3
    data_12 = generate_data(NUM_GREATER_THEN_CLASS_3,['HINDI','ENGLISH','MATHS','SCIENCE','SOCIAL SCIENCE'])
    data = np.vstack([data_3,data_12])

    df = pd.DataFrame(data,columns=['School ID','District','Block','Cluster','Student Id Pseb','Student Roll No.','Grade','Subject','Assesment Type'])

    # add stream
    df['Stream'] = df['Grade'].apply(lambda x:np.nan if x<=10 else rnd.choice(['Science','Arts','Commerce']))

    # add max marks
    df['Max Marks'] = 100

    df['Total Marks Obtained'] = get_marks(df)

    # append pass or fail
    df['Pass/Fail Status'] = df['Total Marks Obtained'].apply(lambda x:"Pass" if x>=33 else "Fail")
    
    # append a columns for year
    df['year'] = np.random.randint(0,10,len(df)) + 2013

    df.to_csv(f'./Data/fake_education_data_{iter_number}.csv',index=False)

for i in range(1,270):
    save_df(i)
    print(ID_START)

