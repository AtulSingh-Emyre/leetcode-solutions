class Solution {
    public int[] leftRightDifference(int[] nums) {
        int n = nums.length;
        int[] lsum = new int[n+1];
        int[] rsum = new int[n+1];
        int[] res = new int[n];
        for(int i=1;i<=n;i++) {
            lsum[i] += lsum[i-1] + nums[i-1];
        }
        for(int i=n-1;i>=0;i--) {
            rsum[i] += rsum[i+1] + nums[i];
        }
        for(int i=0;i<n;i++) {
            res[i] = Math.abs(lsum[i+1] - rsum[i]);
        }
        return res;
    }
}