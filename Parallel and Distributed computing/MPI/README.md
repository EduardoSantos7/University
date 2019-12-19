Requirements:
- Numpy >= 1.16.3

**Run**

mpirun -np NUMBER_OF_PROCESSES python3 project2.py

Example:

        mpirun -np 4 python3 project2.py

The file project2.py reads the file input.txt in which the input can be changed manually or using
the random_matrix_generator.py which can receive 5 arguments to personalize the output, by default
it creates a matrix of 10x10 with numbers in range 0 to 10.

**Input**
- Without args:
```
python3 random_matrix_generator.py
```
- With args example:
```
python3 random_matrix_generator.py -n in.txt -r 10 -c 10 -s 1 -e 200
```
**Output**

```
5 8 9 5 0 0 1 7 6 9
2 4 5 2 4 2 4 7 7 9
1 7 0 6 9 9 7 6 9 1
0 1 8 8 3 9 8 7 3 6
5 1 9 3 4 8 1 4 0 3
9 2 0 4 9 2 7 7 9 8
6 9 3 7 7 4 5 9 3 6
8 0 2 7 7 9 7 3 0 8
7 7 1 1 3 0 8 6 4 5
6 2 5 7 8 4 4 7 7 4
```