#include <iostream>

#else
#endif

int main()
{
#ifdef LINUX
	#if A
	std::cout<<"A";
	#elif B
	std::cout<<"B";
	#elif C
	#else
	std::cout<<"something else";
	#endif
	
#else
	#ifdef ANDROID
	__android_log_print("ANDROID");
	#endif
	int c;
#endif
#if 1
	return 0;
}