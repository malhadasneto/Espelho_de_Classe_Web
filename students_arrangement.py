from random import shuffle


def final_classroom(st_dict, st_front, st_back, st_enemies, classroom_x, classroom_y):
    classroom_final = [[""] * classroom_x for i in range(classroom_y)]
    for k in sorted(st_dict):
        st_dict[int(k)] = st_dict.pop(k)


    #enemies dictionary
    enemies_dict = dict.fromkeys(st_dict)
    for i in enemies_dict:
        temp = []
        for st_group in st_enemies:
            if i in st_group:
                for x in st_group:
                    if x != i:
                        temp.append(x)
        enemies_dict[i] = temp

    # organizing enemies in one list (for priorities below)
    st_enemies_list = []
    for i in range(len(st_enemies)):
        for j in range(len(st_enemies[i])):
            st_enemies_list.append(st_enemies[i][j])

    #find students in the list
    def get_index(list, student):
        for i, sublist in enumerate(list):
            if student in sublist:
                return [i, sublist.index(student)]

    #check if there are students he/she must avoid
    def check_enemies(st,i,j):
        temp_enemies = enemies_dict[st]
        for x in temp_enemies:
            if get_index(classroom_final, x): #se inimigo nao foi posicionado, nao precisa se preocupar
                if abs(i - get_index(classroom_final, x)[0]) < 2 and abs (j - get_index(classroom_final, x)[1]) < 2:
                    return True


    def no_seat(classroom_final):
        c=0
        if len(st_dict) < 11 and classroom_y*classroom_x > 2:
            c += 3
        for i in range(classroom_y-1, -1,-1):
            for j in range (classroom_x-1, -1, -1):
                if classroom_y * classroom_x == len(st_dict) + c:
                    return classroom_final
                classroom_final[i][j] = "  "
                c += 1

    #Arranging students!
    all_lists = []
    for st in st_back+st_front+st_enemies_list+sorted(list(st_dict.keys())):
        if st not in all_lists:
            all_lists.append(st)
    students_in_place = count = 0
    while students_in_place < len(st_dict):
        count += 1
        if count > 100: #if not possible after the first try, reset everything, shuffle, try again
            shuffle(all_lists)
            if count < 400: #max 400 tries, put st where it´s possible
                classroom_final = [[""] * classroom_x for i in range(classroom_y)]
                students_in_place = 0
        no_seat(classroom_final) #when there´s too many empty seats, avoid
        for st in all_lists:
            control = 0
            if get_index(classroom_final, st) is None:
                if st in st_back:
                    start_y = classroom_y-1
                    start_x = classroom_x-1
                    stop_x = stop_y = step = -1
                else:
                    start_x = start_y = 0
                    stop_x = classroom_x
                    stop_y = classroom_y
                    step = 1
                for i in range(start_y, stop_y, step):
                    if control == 0:
                        for j in range(start_x, stop_x, step):
                            if classroom_final[i][j] == "":
                                if count == 400 or check_enemies(st, i, j) != True:
                                    classroom_final[i][j] = st
                                    students_in_place += 1
                                    control = -1
                                    break
        print(count, "count", classroom_final, students_in_place, "st place", len(st_dict), "dict")
    new_list = []
    for sublist in classroom_final:
        new_sublist = []
        for element in sublist:
            if element in st_dict:
                new_sublist.append(st_dict[element])
            else:
                new_sublist.append("  ")
        new_list.append((new_sublist))
    if count >= 100:
        return new_list, "failed"
    return new_list, "ok"
