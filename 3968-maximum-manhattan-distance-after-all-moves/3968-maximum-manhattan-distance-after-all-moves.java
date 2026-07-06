class Solution {
    public int maxDistance(String moves) {
        int x = 0;
        int y = 0;
        int cnt = 0;
        for(char c: moves.toCharArray()) {
            if(c=='U') y++;
            if(c=='D') y--;
            if (c=='L') x++;
            if(c=='R') x--;
            if(c=='_') cnt++;
        }
        return Math.abs(x) + Math.abs(y) + cnt;
    }

}