public class binary {
   private static boolean check(String var0) {
      if (var0.length() == 34) {
         int var10001 = var0.charAt(0);
         int var10000 = 31 ^ var10001;
         var10001 = 31 ^ var10001;
         if (var10000 + 7 == 115 && (73 - var0.charAt(1) ^ 11) == -46 && (var0.charAt(2) + 5 ^ 22) == 98 && 19 - var0.charAt(3) + 51 == -41) {
            var10001 = var0.charAt(4);
            var10000 = 94 ^ var10001;
            var10001 = 94 ^ var10001;
            if (var10000 + 13 == 66 && (37 - var0.charAt(5) ^ 23) == -69 && (var0.charAt(6) + 17 ^ 12) == 128 && 3 - var0.charAt(7) + 83 == -15) {
               var10001 = var0.charAt(8);
               var10000 = 41 ^ var10001;
               var10001 = 41 ^ var10001;
               if (var10000 + 29 == 124 && (66 - var0.charAt(9) ^ 9) == -44 && (var0.charAt(10) + 21 ^ 9) == 142 && 15 - var0.charAt(11) + 55 == -25) {
                  var10001 = var0.charAt(12);
                  var10000 = 88 ^ var10001;
                  var10001 = 88 ^ var10001;
                  if (var10000 + 27 == 69 && (14 - var0.charAt(13) ^ 31) == -74 && (var0.charAt(14) + 7 ^ 79) == 50 && 25 - var0.charAt(15) + 33 == -43) {
                     var10001 = var0.charAt(16);
                     var10000 = 61 ^ var10001;
                     var10001 = 61 ^ var10001;
                     if (var10000 + 11 == 90 && (27 - var0.charAt(17) ^ 17) == -71 && (var0.charAt(18) + 13 ^ 48) == 66 && 25 - var0.charAt(19) + 88 == 13) {
                        var10001 = var0.charAt(20);
                        var10000 = 32 ^ var10001;
                        var10001 = 32 ^ var10001;
                        if (var10000 + 9 == 136 && (69 - var0.charAt(21) ^ 28) == -57 && (var0.charAt(22) + 12 ^ 13) == 96 && 31 - var0.charAt(23) + 50 == -37) {
                           var10001 = var0.charAt(24);
                           var10000 = 87 ^ var10001;
                           var10001 = 87 ^ var10001;
                           if (var10000 + 15 == 69 && (31 - var0.charAt(25) ^ 34) == -62 && (var0.charAt(26) + 18 ^ 68) == 23 && 37 - var0.charAt(27) + 12 == -5) {
                              var10001 = var0.charAt(28);
                              var10000 = 49 ^ var10001;
                              var10001 = 49 ^ var10001;
                              if (var10000 + 21 == 27 && (86 - var0.charAt(29) ^ 5) == -15 && (var0.charAt(30) + 24 ^ 30) == 105 && 8 - var0.charAt(31) + 67 == 18) {
                                 var10001 = var0.charAt(32);
                                 var10000 = 11 ^ var10001;
                                 var10001 = 11 ^ var10001;
                                 if (var10000 + 27 == 85 && (48 - var0.charAt(33) ^ 11) == -72) {
                                    return true;
                                 }
                              }
                           }
                        }
                     }
                  }
               }
            }
         }
      }

      return false;
   }

   public static void main(String[] var0) {
      if (var0.length == 0) {
         System.out.println("Usage: java binary <flag>");
      } else {
         if (check(var0[0])) {
            System.out.println("Correct!");
         } else {
            System.out.println("Incorrect.");
         }

      }
   }
}
