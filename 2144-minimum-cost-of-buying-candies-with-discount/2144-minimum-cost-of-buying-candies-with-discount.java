class Solution {
    public int minimumCost(int[] cost) {
      Arrays.sort(cost);
      int res = 0;
      int cnt = 0;
      for(int i = cost.length-1; i>=0 ; i--) {
        if(cnt<2) {
            res+=cost[i];
            cnt++;
        } 
        else {
            cnt = 0;
        }
      }  
      return res;
    }
}