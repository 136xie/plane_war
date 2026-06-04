#include<stdio.h>
#define STUDENT_NUM 4
#define COURSE_NUM 5
int main() { 
	int id;
	char name[50];
	int student_score[COURSE_NUM];
	double average;
	FILE* fp = fopen("D:\\StudentGrade.txt.txt", "w");
	for (int i = 0; i < STUDENT_NUM;i++) {
		scanf("%d %s %d %d %d %d %d", &id, name, &student_score[0], &student_score[1], &student_score[2], &student_score[3], &student_score[4]);
		int sum = 0;
		for (int j = 0; j < 5; j++) {
