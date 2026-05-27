class Solution {
    public boolean canReach(String s, int minJump, int maxJump) {
        int L = s.length();
        // If the last character is '1', we can never reach it
        if (s.charAt(L - 1) == '1') return false;

        // dp[i] will be true if index i is reachable
        boolean[] dp = new boolean[L];
        dp[0] = true; // We start at index 0

        // tracks the count of reachable indices in the current window
        int reachableCount = 0; 

        for (int i = 1; i < L; i++) {
            // Add the new index entering the window from the right side
            if (i >= minJump && dp[i - minJump]) {
                reachableCount++;
            }
            
            // Remove the old index leaving the window from the left side
            if (i > maxJump && dp[i - maxJump - 1]) {
                reachableCount--;
            }

            // i is reachable if it's '0' and there's at least one valid jump source
            if (s.charAt(i) == '0' && reachableCount > 0) {
                dp[i] = true;
            }
        }

        return dp[L - 1];
    }
}
