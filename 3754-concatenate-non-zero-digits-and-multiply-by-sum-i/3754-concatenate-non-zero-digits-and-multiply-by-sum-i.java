class Solution {
    public long sumAndMultiply(int n) {
        if(n==0) return 0;
        String s = n+"";
        StringBuilder sb = new StringBuilder();
        long sum = 0;
        while(n>0) {
            int dig = n%10;
            if(dig!=0) sb.append(dig);
            sum+=dig;
            n/=10;
        }
        long res = Long.parseLong(sb.reverse().toString()) * sum;
        return res;
    }
}