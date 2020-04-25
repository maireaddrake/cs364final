// Test #1 Euler project problem 1
int sum_3_or_5(int n) {
 int sum;
 int i;
 sum = 0;
 i = 0;
 while (i < n) {
 if (i % 3 == 0 || i % 5 == 0)
 sum = sum + i;

 i = i + 1;
 }
 return sum;
}
int main() {
 print("The answer is: ", sum_3_or_5(1000), "Woot!");
}
/*
// Test #2 A program that determines if
// a number n is prime
int main() {
 bool prime;
 int i;
 int n;
 i = 2; // where to start checking divisors
 n = 1234567; // number checking to see if prime
 prime = true;
 while (prime && i < n/2.0) {
 if (n % i == 0) // is n divisible by i?
 prime = false;
 i = i + 1;
 }
 print(i-1);
}
*/