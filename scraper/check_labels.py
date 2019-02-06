def main():
    with open('course_labels.txt', 'r+') as f:
        data = f.read()

    data = data.split('\n')

    data = [d.split('\t') for d in data]

    count_misc = 0

    courses = []

    for d in data:
        courses.append(d[1])
        if d[1] == 'Misc.':
            count_misc += 1

    print(set(courses))
    print('misc =', count_misc)
    print('total =', len(data))

if __name__ == '__main__':
    main()