# sanity check to make sure there are enough labels and that they make sense

def main():
    with open('labels.txt', 'r+') as f:
        data = f.read()

    data = data.split('\n')
    data = [d.split('\t') for d in data]
    
    count_misc = 0
    courses = []

    # iterate through the labels and count misc. ones
    for d in data:
        courses.append(d[1])
        if d[1] == 'Misc.':
            count_misc += 1

    print('List of labels:', set(courses), ', total of ', len(set(courses)))
    print('Misc =', count_misc)
    print('Total =', len(data))

if __name__ == '__main__':
    main()