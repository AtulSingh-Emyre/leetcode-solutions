class Solution {
    public int maxIceCream(int[] costs, int coins) {
        int res = 0;
        Arrays.sort(costs);
        for(int c: costs) {
            if(c<=coins) {
                coins-=c;
                res++;
            } else break;
        }
        return res;
    }
}