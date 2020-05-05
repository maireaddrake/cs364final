int main() {
    float epsilon;
    float r;
	float tmp;
	float n;
	n = 2.0;
    //epsilon	= 1e-6;
    epsilon = 0.000006;
	r = n;

    if (r*r - n < 0)
		tmp = n - r*r;

    while (tmp > epsilon) {
        r = (r + n/r)/2.0;
        if (r*r - n < 0)
            tmp = n - r*r;
    }
    print(r);
}