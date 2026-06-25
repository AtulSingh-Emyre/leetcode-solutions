class Solution {
    public int countMajoritySubarrays(int[] nums, int target) {
        int n  = nums.length;
        int res = 0;
        for(int i = 0;i<n;i++) {
            int sum = 0;
            for(int j = i;j<n;j++) {
                if(nums[j] == target) sum++;
                if(sum>(j-i+1)/2) res++;
            }
        }
        return res;
    }
}