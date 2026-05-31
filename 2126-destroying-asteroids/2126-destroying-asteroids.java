class Solution {
    public boolean asteroidsDestroyed(int mass, int[] asteroids) {
        Arrays.sort(asteroids);
        int m = asteroids.length-1;
        for(int a: asteroids) {
            if(mass<a) return false;
            if(mass>=asteroids[m]) return true;
            if(mass+a<mass) mass = Integer.MAX_VALUE;
            else mass+=a;
        }
        return true;

    }
}