#include <stdio.h>

int main(){
    int arr[5] = {29,14,10,37,14};
    int n = 5;

    // comparing the key elements with its predecessor and swapping if the predecessor is greater than the key element and doing this till j reduces to zero(0) 
    
    for (int i = 0; i < n;i++){
        int key = arr[i];
        int j = i - 1;
        while (arr[j]>key && j>= 0){
            arr[j+1] = arr[j];
            j = j - 1;
        }
        arr[j+1]= key;
    }

    // printing the elements after sorting....
    for(int i = 0; i < n ; i++){
        printf("%d \n", arr[i]);
    }
}