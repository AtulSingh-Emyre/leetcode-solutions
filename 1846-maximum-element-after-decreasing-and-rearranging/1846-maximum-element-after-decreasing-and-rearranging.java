class Solution {
    public int maximumElementAfterDecrementingAndRearranging(int[] arr) {
        Arrays.sort(arr);
        int max = 0;
        for(int a:arr) {
            if(a==max) continue;
            if(a>max) max++;
        }
        return max;
    }

}