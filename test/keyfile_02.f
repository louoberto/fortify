      !     euclid.f (FORTRAN 77)
      !     Find greatest common divisor using the Euclidean algorithm

      program euclid
         print *, 'A?'
         read *, na
         if (na .le. 0) then
            print *, 'A must be a positive integer.'
            stop
         endif
         print *, 'B?'
         read *, nb
         if (nb .le. 0) then
            print *, 'B must be a positive integer.'
            stop
         endif
         print *, 'The GCD of', na, ' and', nb, ' is', ngcd(na, nb), '.'
         stop
      end

      function ngcd(na, nb)
         ia = na
         ib = nb
1        if (ib .ne. 0) then
            itemp = ia
            ia = ib
            ib = mod(itemp, ib)
            goto 1
         endif
         ngcd = ia
         return
      end