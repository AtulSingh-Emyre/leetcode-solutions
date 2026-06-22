class Solution {
    public int maxNumberOfBalloons(String text) {
        int[] fr = new int[26];
        for(char c: text.toCharArray()) fr[c-'a']++;
        int n = fr['b'-'a'];
        n = Math.min(n, fr[0]);
        n = Math.min(n,fr['l'-'a']/2);
        n = Math.min(n,fr['o'-'a']/2);
        n = Math.min(n,fr['n'-'a']);
        return n;
    }
}