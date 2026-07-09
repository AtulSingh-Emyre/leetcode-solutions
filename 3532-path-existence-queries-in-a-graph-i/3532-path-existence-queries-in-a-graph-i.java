class Solution {
    public boolean[] pathExistenceQueries(int n, int[] nums, int maxDiff, int[][] queries) {
        int[] t = new int[n];
        for(int i=1;i<n;i++) {
            if(nums[i]-nums[i-1]>maxDiff) t[i] = t[i-1]+1;
            else t[i] = t[i-1];
            // System.out.println(nums[i]-nums[i-1]);
        }
        // System.out.println(Arrays.toString(t));
        boolean[] res = new boolean[queries.length];
        for(int i = 0;i<res.length;i++) {
            int[] q = queries[i];
            if(t[q[0]] == t[q[1]]) res[i] = true;
            else res[i] = false;
        }
        
        return res;
        
    }
}