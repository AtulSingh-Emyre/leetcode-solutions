class Solution {
    public boolean asteroidsDestroyed(int mass, int[] asteroids) {
        Arrays.sort(asteroids);
        for(int a: asteroids) {
            if(mass<a) return false;
            if(mass+a<mass) mass = Integer.MAX_VALUE;
            else mass+=a;
        }
        return true;

    }
}