class Solution {
    public int minElement(int[] nums) {
        int result = Integer.MAX_VALUE;
        for(int n: nums) {
            int sumD = 0;
            while (n>0) {
                sumD += n%10;
                n/=10;
            }
            result = Math.min(sumD,result);
        }
        return result;
    }
}